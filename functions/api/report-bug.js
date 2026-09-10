export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    // 1. Origin Security Check: if Origin header exists, verify it matches allowed domains
    const origin = request.headers.get("Origin");
    if (origin) {
      const allowedOrigins = [
        "https://doc-inspector.com",
        "https://www.doc-inspector.com",
        "http://localhost",
        "http://127.0.0.1"
      ];
      const isAllowed = allowedOrigins.some(o => origin.startsWith(o));
      if (!isAllowed) {
        return new Response(JSON.stringify({ error: "Access Denied: Forbidden Origin" }), {
          status: 403,
          headers: { "Content-Type": "application/json" }
        });
      }
    }

    // 2. Client Secret Authorization Check
    const clientSecret = request.headers.get("X-DocInspector-Secret");
    if (clientSecret !== "DocInspector_WPF_Client_2026_Secure") {
      return new Response(JSON.stringify({ error: "Unauthorized access" }), {
        status: 401,
        headers: { "Content-Type": "application/json" }
      });
    }

    // 3. IP-based Rate Limiting (using optional RATE_LIMIT_KV binding)
    const clientIp = request.headers.get("CF-Connecting-IP") || "unknown";
    if (env.RATE_LIMIT_KV) {
      const currentHour = new Date().toISOString().substring(0, 13); // "YYYY-MM-DDTHH"
      const limitKey = `ratelimit_${clientIp}_${currentHour}`;
      
      const countVal = await env.RATE_LIMIT_KV.get(limitKey);
      const count = countVal ? parseInt(countVal, 10) : 0;
      
      if (count >= 5) {
        return new Response(JSON.stringify({ error: "Rate limit exceeded. Maximum 5 reports per hour." }), {
          status: 429,
          headers: { "Content-Type": "application/json" }
        });
      }
      
      // Store count and set TTL for 1 hour (3600 seconds)
      await env.RATE_LIMIT_KV.put(limitKey, (count + 1).toString(), { expirationTtl: 3600 });
    }

    // 4. Parse Multipart Form Data
    const formData = await request.formData();
    const message = formData.get("message") || "";
    const systemInfo = formData.get("systemInfo") || "";
    const logs = formData.get("logs") || "";
    const licenseKey = formData.get("licenseKey") || "Unlicensed / Trial";
    const clientEmail = (formData.get("email") || "").trim();
    const lang = (formData.get("lang") || "en").toLowerCase();
    
    const fileFields = [
      ...formData.getAll("files"),
      ...formData.getAll("file"),
      ...formData.getAll("attachment")
    ];

    const attachments = [];
    let totalSize = 0;

    // 5. Process attachments
    for (const file of fileFields) {
      if (file && file instanceof File && file.size > 0) {
        // Individual file limit: 20MB
        if (file.size > 20 * 1024 * 1024) {
          return new Response(JSON.stringify({ error: `File ${file.name} exceeds the 20MB limit` }), {
            status: 400,
            headers: { "Content-Type": "application/json" }
          });
        }

        totalSize += file.size;
        // Total files limit: 50MB
        if (totalSize > 50 * 1024 * 1024) {
          return new Response(JSON.stringify({ error: "Total attachment size exceeds the 50MB limit" }), {
            status: 400,
            headers: { "Content-Type": "application/json" }
          });
        }

        const cleanFileName = file.name.replace(/[^a-zA-Z0-9.\-_]/g, "_");
        const fileKey = `bug_${Date.now()}_${Math.random().toString(36).substring(2, 8)}_${cleanFileName}`;

        // Upload to R2 Bucket
        if (env.BUG_REPORTS_BUCKET) {
          await env.BUG_REPORTS_BUCKET.put(fileKey, file.stream(), {
            httpMetadata: { contentType: file.type }
          });

          const tokenParam = encodeURIComponent("Vlad$$395");
          attachments.push({
            name: file.name,
            sizeMb: (file.size / 1024 / 1024).toFixed(2),
            url: `https://doc-inspector.com/api/download-bug?file=${encodeURIComponent(fileKey)}&token=${tokenParam}`
          });
        }
      }
    }

    // 6. Construct Attachments HTML Block (Sent ONLY to Admin)
    let attachmentsHtml = '<p style="color: #777;">None</p>';
    if (attachments.length > 0) {
      attachmentsHtml = '<ul style="padding-left: 20px; margin: 10px 0;">';
      for (const att of attachments) {
        attachmentsHtml += `
          <li style="margin-bottom: 8px;">
            <a href="${att.url}" style="color: #0078d4; text-decoration: none; font-weight: bold;">Download ${att.name}</a> 
            <span style="color: #666; font-size: 12.5px;">(${att.sizeMb} MB - Securizat &amp; expira in 7 zile)</span>
          </li>
        `;
      }
      attachmentsHtml += '</ul>';
    }

    // 7. Construct Admin Notification Email HTML Content
    const htmlContent = `
      <div style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto; border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
        <h2 style="color: #0078d4; border-bottom: 2px solid #0078d4; padding-bottom: 8px; margin-top: 0;">DocInspector Bug Report</h2>
        
        <p><strong>License Status:</strong> <span style="background: #f1f1f1; padding: 3px 8px; border-radius: 4px; font-weight: bold;">${licenseKey}</span></p>
        <p><strong>User Email:</strong> <span style="background: #f1f1f1; padding: 3px 8px; border-radius: 4px; font-weight: bold;">${clientEmail || "Not provided"}</span></p>
        <p><strong>Language:</strong> <span style="background: #f1f1f1; padding: 3px 8px; border-radius: 4px; font-weight: bold;">${lang.toUpperCase()}</span></p>
        
        <p><strong>User Description:</strong></p>
        <div style="background: #f9f9f9; border-left: 4px solid #0078d4; padding: 12px; margin: 10px 0; font-style: italic; white-space: pre-wrap;">${message}</div>
        
        <p><strong>System Details:</strong></p>
        <pre style="background: #f4f4f4; padding: 12px; border-radius: 4px; font-size: 13px; overflow-x: auto; white-space: pre-wrap; font-family: Consolas, monospace;">${systemInfo}</pre>
        
        <p><strong>Attachments (${attachments.length}):</strong></p>
        ${attachmentsHtml}
        
        <p><strong>Application Logs:</strong></p>
        <pre style="background: #1e1e1e; color: #d4d4d4; padding: 12px; border-radius: 4px; font-size: 12px; max-height: 350px; overflow-y: auto; font-family: Consolas, monospace; white-space: pre-wrap;">${logs || "No logs attached."}</pre>
      </div>
    `;

    // 8. Send Email to Admin via Resend API
    const cleanSnippet = message.replace(/[\r\n\t]+/g, " ").trim().substring(0, 50);
    const emailSubject = `[Bug Report] DocInspector - ${cleanSnippet || "User Feedback"}`;

    const emailPayload = {
      from: env.SENDER_EMAIL || "DocInspector Support <support@doc-inspector.com>",
      to: env.RECEIVER_EMAIL || "support@doc-inspector.com",
      reply_to: clientEmail || "support@doc-inspector.com",
      subject: emailSubject,
      html: htmlContent
    };

    const resendApiKey = env.RESEND_API_KEY;
    if (!resendApiKey) {
      return new Response(JSON.stringify({ error: "Missing RESEND_API_KEY in environment variables" }), {
        status: 500,
        headers: { "Content-Type": "application/json" }
      });
    }

    const resendResponse = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${resendApiKey}`,
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

    // 9. Send Localized Auto-Reply Confirmation to Client via Resend API
    if (clientEmail && clientEmail.includes("@")) {
      let autoReplySubject = "";
      let autoReplyHtml = "";

      if (lang === "ro") {
        autoReplySubject = "Confirmare primire raport eroare — DocInspector";
        autoReplyHtml = `
          <div style="font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <div style="background: #0a1628; padding: 24px; text-align: center; border-bottom: 3px solid #06b6d4;">
              <h1 style="color: #22d3ee; margin: 0; font-size: 24px; font-weight: 800; letter-spacing: -0.5px;">DocInspector Pro</h1>
              <p style="color: #94a3b8; font-size: 13px; margin: 4px 0 0 0;">Centru de Suport Tehnic</p>
            </div>
            <div style="padding: 32px; background: #ffffff; line-height: 1.6;">
              <h2 style="color: #0f172a; margin-top: 0; font-size: 20px; font-weight: 700;">Bună ziua,</h2>
              <p style="font-size: 15px; color: #334155;">Am primit cu succes raportul dumneavoastră de eroare / feedback.</p>
              <p style="font-size: 15px; color: #334155;">Echipa noastră tehnică analizează deja datele de diagnostic și fișierele trimise. Vom reveni cu un răspuns detaliat sau o soluție în cel mai scurt timp posibil.</p>
              <div style="margin: 24px 0; padding: 16px; background: #f8fafc; border-left: 4px solid #06b6d4; border-radius: 4px; font-size: 14px; color: #475569;">
                💡 <strong>Notă:</strong> Dacă doriți să adăugați detalii sau capturi de ecran suplimentare, puteți răspunde direct la acest email.
              </div>
              <p style="font-size: 15px; color: #334155; margin-bottom: 0;">Cu respect,<br /><strong>Echipa DocInspector Support</strong><br /><a href="https://doc-inspector.com" style="color: #0284c7; text-decoration: none;">https://doc-inspector.com</a></p>
            </div>
            <div style="background: #f1f5f9; padding: 16px; text-align: center; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0;">
              © 2026 DocInspector. Toate drepturile rezervate.
            </div>
          </div>
        `;
      } else if (lang === "ru") {
        autoReplySubject = "Подтверждение получения отчета об ошибке — DocInspector";
        autoReplyHtml = `
          <div style="font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <div style="background: #0a1628; padding: 24px; text-align: center; border-bottom: 3px solid #06b6d4;">
              <h1 style="color: #22d3ee; margin: 0; font-size: 24px; font-weight: 800; letter-spacing: -0.5px;">DocInspector Pro</h1>
              <p style="color: #94a3b8; font-size: 13px; margin: 4px 0 0 0;">Центр технической поддержки</p>
            </div>
            <div style="padding: 32px; background: #ffffff; line-height: 1.6;">
              <h2 style="color: #0f172a; margin-top: 0; font-size: 20px; font-weight: 700;">Здравствуйте,</h2>
              <p style="font-size: 15px; color: #334155;">Мы успешно получили ваш отчет об ошибке / обратную связь.</p>
              <p style="font-size: 15px; color: #334155;">Наша техническая команда уже анализирует диагностические данные и логи приложения. Мы свяжемся с вами с решением или ответом в кратчайшие сроки.</p>
              <div style="margin: 24px 0; padding: 16px; background: #f8fafc; border-left: 4px solid #06b6d4; border-radius: 4px; font-size: 14px; color: #475569;">
                💡 <strong>Примечание:</strong> Если вы хотите добавить дополнительную информацию или скриншоты, просто ответьте на это письмо.
              </div>
              <p style="font-size: 15px; color: #334155; margin-bottom: 0;">С уважением,<br /><strong>Команда поддержки DocInspector</strong><br /><a href="https://doc-inspector.com" style="color: #0284c7; text-decoration: none;">https://doc-inspector.com</a></p>
            </div>
            <div style="background: #f1f5f9; padding: 16px; text-align: center; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0;">
              © 2026 DocInspector. Все права защищены.
            </div>
          </div>
        `;
      } else {
        autoReplySubject = "Bug Report Confirmation — DocInspector";
        autoReplyHtml = `
          <div style="font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <div style="background: #0a1628; padding: 24px; text-align: center; border-bottom: 3px solid #06b6d4;">
              <h1 style="color: #22d3ee; margin: 0; font-size: 24px; font-weight: 800; letter-spacing: -0.5px;">DocInspector Pro</h1>
              <p style="color: #94a3b8; font-size: 13px; margin: 4px 0 0 0;">Technical Support Desk</p>
            </div>
            <div style="padding: 32px; background: #ffffff; line-height: 1.6;">
              <h2 style="color: #0f172a; margin-top: 0; font-size: 20px; font-weight: 700;">Hello,</h2>
              <p style="font-size: 15px; color: #334155;">We have successfully received your bug report / feedback.</p>
              <p style="font-size: 15px; color: #334155;">Our engineering team is already analyzing the diagnostic logs and system details. We will get back to you with an update or resolution as quickly as possible.</p>
              <div style="margin: 24px 0; padding: 16px; background: #f8fafc; border-left: 4px solid #06b6d4; border-radius: 4px; font-size: 14px; color: #475569;">
                💡 <strong>Note:</strong> If you have any additional information or screenshots to share, feel free to reply directly to this email.
              </div>
              <p style="font-size: 15px; color: #334155; margin-bottom: 0;">Best regards,<br /><strong>DocInspector Support Team</strong><br /><a href="https://doc-inspector.com" style="color: #0284c7; text-decoration: none;">https://doc-inspector.com</a></p>
            </div>
            <div style="background: #f1f5f9; padding: 16px; text-align: center; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0;">
              © 2026 DocInspector. All rights reserved.
            </div>
          </div>
        `;
      }

      try {
        await fetch("https://api.resend.com/emails", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${resendApiKey}`,
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            from: env.SENDER_EMAIL || "DocInspector Support <support@doc-inspector.com>",
            to: clientEmail,
            reply_to: "support@doc-inspector.com",
            subject: autoReplySubject,
            html: autoReplyHtml
          })
        });
      } catch (err) {
        console.error("Auto-reply email error:", err);
      }
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
