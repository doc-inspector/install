export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    // 1. Simple Security Check: verify client secret header
    const clientSecret = request.headers.get("X-DocInspector-Secret");
    if (clientSecret !== "DocInspector_WPF_Client_2026_Secure") {
      return new Response(JSON.stringify({ error: "Unauthorized access" }), {
        status: 401,
        headers: { "Content-Type": "application/json" }
      });
    }

    // 2. Parse Multipart Form Data
    const formData = await request.formData();
    const message = formData.get("message") || "";
    const systemInfo = formData.get("systemInfo") || "";
    const logs = formData.get("logs") || "";
    const licenseKey = formData.get("licenseKey") || "Unlicensed / Trial";
    const file = formData.get("file");

    let fileKey = "";
    let downloadUrl = "";

    // 3. Process Attachment if present
    if (file && file instanceof File && file.size > 0) {
      // Security: Limit file size to 20MB
      if (file.size > 20 * 1024 * 1024) {
        return new Response(JSON.stringify({ error: "Attachment exceeds 20MB size limit" }), {
          status: 400,
          headers: { "Content-Type": "application/json" }
        });
      }

      // Generate a unique clean filename
      const cleanFileName = file.name.replace(/[^a-zA-Z0-9.\-_]/g, "_");
      fileKey = `bug_${Date.now()}_${cleanFileName}`;

      // Upload to R2 Bucket (BUG_REPORTS_BUCKET)
      await env.BUG_REPORTS_BUCKET.put(fileKey, file.stream(), {
        httpMetadata: { contentType: file.type }
      });

      // Construct secure download URL through our API
      downloadUrl = `https://doc-inspector.com/api/download-bug?file=${fileKey}`;
    }

    // 4. Construct Email HTML Content
    const htmlContent = `
      <div style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto; border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
        <h2 style="color: #0078d4; border-bottom: 2px solid #0078d4; padding-bottom: 8px; margin-top: 0;">DocInspector Bug Report (v3.0.1)</h2>
        
        <p><strong>License Status:</strong> <span style="background: #f1f1f1; padding: 3px 8px; border-radius: 4px; font-weight: bold;">${licenseKey}</span></p>
        
        <p><strong>User Description:</strong></p>
        <div style="background: #f9f9f9; border-left: 4px solid #0078d4; padding: 12px; margin: 10px 0; font-style: italic; white-space: pre-wrap;">${message || "No description provided."}</div>
        
        <p><strong>System Details:</strong></p>
        <pre style="background: #f4f4f4; padding: 12px; border-radius: 4px; font-size: 13px; overflow-x: auto; white-space: pre-wrap; font-family: Consolas, monospace;">${systemInfo || "N/A"}</pre>
        
        <p><strong>Attachment:</strong></p>
        ${fileKey 
          ? `<p><a href="${downloadUrl}" style="background: #0078d4; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; display: inline-block; font-weight: bold;">Download ${file.name}</a> (${(file.size / 1024 / 1024).toFixed(2)} MB)</p>`
          : `<p style="color: #777;">None</p>`
        }
        
        <p><strong>Application Logs:</strong></p>
        <pre style="background: #1e1e1e; color: #d4d4d4; padding: 12px; border-radius: 4px; font-size: 12px; max-height: 350px; overflow-y: auto; font-family: Consolas, monospace; white-space: pre-wrap;">${logs || "No logs attached."}</pre>
      </div>
    `;

    // 5. Send Email via Resend API
    const emailPayload = {
      from: env.SENDER_EMAIL,
      to: env.RECEIVER_EMAIL,
      subject: `[Bug Report] DocInspector - ${licenseKey}`,
      html: htmlContent
    };

    const resendResponse = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${env.RESEND_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(emailPayload)
    });

    if (!resendResponse.ok) {
      const errorText = await resendResponse.text();
      return new Response(JSON.stringify({ error: `Failed to send email: ${errorText}` }), {
        status: 502,
        headers: { "Content-Type": "application/json" }
      });
    }

    return new Response(JSON.stringify({ success: true, message: "Report submitted successfully" }), {
      status: 200,
      headers: { "Content-Type": "application/json" }
    });

  } catch (error) {
    return new Response(JSON.stringify({ error: `Internal Server Error: ${error.message}` }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
