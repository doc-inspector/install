/**
 * Cloudflare Pages Function: /api/trial-check
 * Handles Hardware-ID (HWID) based Trial verification via Cloudflare KV.
 */
export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }
  });
}

export async function onRequestPost(context) {
  const { request, env } = context;

  const corsHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json"
  };

  try {
    const body = await request.json();
    const { hwid, machine, version } = body || {};

    if (!hwid || typeof hwid !== "string" || hwid.trim().length < 8) {
      return new Response(JSON.stringify({ 
        valid: false, 
        tier: "Unlicensed", 
        trial_days_left: 0, 
        message: "Invalid Hardware Identifier" 
      }), {
        status: 400,
        headers: corsHeaders
      });
    }

    const cleanHwid = hwid.trim().toLowerCase();
    const clientIp = request.headers.get("CF-Connecting-IP") || "unknown";
    const now = new Date();

    // Check if Cloudflare KV is bound
    if (env && env.DOCINSPECTOR_TRIALS) {
      const existingRaw = await env.DOCINSPECTOR_TRIALS.get(cleanHwid);

      if (existingRaw) {
        let record;
        try {
          record = JSON.parse(existingRaw);
        } catch {
          record = { started_at: existingRaw };
        }

        const startedAt = new Date(record.started_at || now);
        const elapsedMs = now.getTime() - startedAt.getTime();
        const elapsedDays = elapsedMs / (1000 * 60 * 60 * 24);

        const TRIAL_TOTAL_DAYS = 3;

        if (elapsedDays <= TRIAL_TOTAL_DAYS) {
          const daysLeft = Math.max(1, Math.ceil(TRIAL_TOTAL_DAYS - elapsedDays));
          return new Response(JSON.stringify({
            valid: true,
            tier: "Trial",
            trial_days_left: daysLeft,
            started_at: record.started_at,
            message: `Trial active. ${daysLeft} day(s) remaining.`
          }), {
            status: 200,
            headers: corsHeaders
          });
        } else {
          return new Response(JSON.stringify({
            valid: false,
            tier: "Unlicensed",
            trial_days_left: 0,
            started_at: record.started_at,
            message: "Trial period has expired on this computer. Please activate a license."
          }), {
            status: 200,
            headers: corsHeaders
          });
        }
      } else {
        // First time this HWID is seen: Register trial
        const newRecord = {
          hwid: cleanHwid,
          started_at: now.toISOString(),
          machine: machine || "Unknown",
          version: version || "3.0.5",
          initial_ip: clientIp
        };

        await env.DOCINSPECTOR_TRIALS.put(cleanHwid, JSON.stringify(newRecord));

        return new Response(JSON.stringify({
          valid: true,
          tier: "Trial",
          trial_days_left: 3,
          started_at: newRecord.started_at,
          message: "Trial started. 3 days remaining."
        }), {
          status: 200,
          headers: corsHeaders
        });
      }
    } else {
      // Fallback if KV binding is not yet attached in dashboard
      return new Response(JSON.stringify({
        valid: true,
        tier: "Trial",
        trial_days_left: 3,
        message: "Trial active (KV pending configuration)"
      }), {
        status: 200,
        headers: corsHeaders
      });
    }

  } catch (err) {
    return new Response(JSON.stringify({ 
      valid: false, 
      tier: "Unlicensed", 
      trial_days_left: 0, 
      message: "Server Error: " + err.message 
    }), {
      status: 500,
      headers: corsHeaders
    });
  }
}