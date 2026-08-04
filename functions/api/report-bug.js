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
    
    // Support files from C# (files / file) and HTML forms (attachment)
    const fileFields = [
      ...formData.getAll("files"),
      ...formData.getAll("file"),
      ...formData.getAll("attachment")
    ];

    const attachments = [];
    let totalSize = 0;

    // 3. Process attachments
    for (const file of fileFields) {
      if (file && file instanceof File && file.size > 0) {
        // Limit individual file size to 20MB
        if (file.size > 20 * 1024 * 1024) {
          return new Response(JSON.stringify({ error: `File ${file.name} exceeds the 20MB limit` }), {
            status: 400,
            headers: { "Content-Type": "application/json" }
          });
        }

        totalSize += file.size;
        // Limit total attachments size to 50MB to prevent overloading R2
        if (totalSize > 50 * 1024 * 1024) {
          return new Response(JSON.stringify({ error: "Total attachment size exceeds the 50MB limit" }), {
            status: 400,
            headers: { "Content-Type": "application/json" }
          });
        }

        // Generate a unique clean filename
        const cleanFileName = file.name.replace(/[^a-zA-Z0-9.\-_]/g, "_");
        const fileKey = `bug_${Date.now()}_${cleanFileName}`;

        // Upload to R2 Bucket
        await env.BUG_REPORTS_BUCKET.put(fileKey, file.stream(), {
          httpMetadata: { contentType: file.type }
        });

        // Store details
        attachments.push({
          name: file.name,
          sizeMb: (file.size / 1024 / 1024).toFixed(2),
          url: `https://doc-inspector.com/api/download-bug?file=${fileKey}`
        });
      }
    }

    // 4. Construct Attachments HTML Block
    let attachmentsHtml = '<p style="color: #777;">None</p>';
    if (attachments.length > 0) {
      attachmentsHtml = '<ul style="padding-left: 20px; margin: 10px 0;">';
      for (const att of attachments) {
        attachmentsHtml += `
          <li style="margin-bottom: 8px;">
            <a href="${att.url}" style="color: #0078d4; text-decoration: none; font-weight: bold;">Download ${att.name}</a> 
            <span style="color: #666; font-size: 12.5px;">(${att.sizeMb} MB)</span>
          </li>
        `;
      }
      attachmentsHtml += '</ul>';
    }

    // 5. Construct Email HTML Content
    const htmlContent = `
      <div style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto; border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
        <h2 style="color: #0078d4; border-bottom: 2px solid #0078d4; padding-bottom: 8px; margin-top: 0;">DocInspector Bug Report (v3.0.1)</h2>
        
        <p><strong>License Status:</strong> <span style="background: #f1f1f1; padding: 3px 8px; border-radius: 4px; font-weight: bold;">${licenseKey}</span></p>
        
        <p><strong>User Description:</strong></p>
        <div style="background: #f9f9f9; border-left: 4px solid #0078d4; padding: 12px; margin: 10px 0; font-style: italic; white-space: pre-wrap;">${message || "No description provided."}</div>
        
        <p><strong>System Details:</strong></p>
        <pre style="background: #f4f4f4; padding: 12px; border-radius: 4px; font-size: 13px; overflow-x: auto; white-space: pre-wrap; font-family: Consolas, monospace;">${systemInfo || "N/A"}</pre>
        
        <p><strong>Attachments (${attachments.length}):</strong></p>
        ${attachmentsHtml}
        
        <p><strong>Application Logs:</strong></p>
        <pre style="background: #1e1e1e; color: #d4d4d4; padding: 12px; border-radius: 4px; font-size: 12px; max-height: 350px; overflow-y: auto; font-family: Consolas, monospace; white-space: pre-wrap;">${logs || "No logs attached."}</pre>
      </div>
    `;

    // 6. Send Email via Resend API
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
