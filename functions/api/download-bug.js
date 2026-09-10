export async function onRequestGet(context) {
  const { request, env } = context;

  try {
    // Parse URL query parameters
    const url = new URL(request.url);
    const fileKey = url.searchParams.get("file");
    const token = url.searchParams.get("token");

    // 1. Validate Secret Token
    if (token !== "Vlad$$395") {
      return new Response("Access Denied: Invalid or missing security token.", {
        status: 401,
        headers: { "Content-Type": "text/plain; charset=utf-8" }
      });
    }

    if (!fileKey) {
      return new Response("Missing file parameter", { status: 400 });
    }

    // 2. Check 7-Day Auto-Expiration (Key format: bug_<timestamp>_<random>_<filename>)
    const parts = fileKey.split("_");
    if (parts.length >= 2) {
      const uploadTimestamp = parseInt(parts[1], 10);
      if (!isNaN(uploadTimestamp)) {
        const SEVEN_DAYS_MS = 7 * 24 * 60 * 60 * 1000;
        if (Date.now() - uploadTimestamp > SEVEN_DAYS_MS) {
          // File has expired: delete from R2 and return 410 Gone
          try {
            if (env.BUG_REPORTS_BUCKET) {
              await env.BUG_REPORTS_BUCKET.delete(fileKey);
            }
          } catch (delErr) {
            console.error("Failed to delete expired R2 file:", delErr);
          }
          return new Response("This attachment has expired and was automatically deleted after 7 days.", {
            status: 410,
            headers: { "Content-Type": "text/plain; charset=utf-8" }
          });
        }
      }
    }

    // 3. Retrieve file object from Cloudflare R2
    const object = await env.BUG_REPORTS_BUCKET.get(fileKey);

    if (!object) {
      return new Response("File not found in storage (it may have been deleted or expired).", { status: 404 });
    }

    // Prepare response headers
    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set("etag", object.httpEtag);
    
    let originalName = fileKey;
    const nameIndex = fileKey.indexOf("_", 4);
    if (nameIndex !== -1) {
      originalName = fileKey.substring(nameIndex + 1);
    }
    headers.set("Content-Disposition", `attachment; filename="${originalName}"`);

    // Return the R2 object body
    return new Response(object.body, {
      headers
    });

  } catch (error) {
    return new Response(`Error retrieving file: ${error.message}`, { status: 500 });
  }
}
