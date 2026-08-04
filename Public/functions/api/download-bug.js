export async function onRequestGet(context) {
  const { request, env } = context;

  try {
    // Parse URL query parameter
    const url = new URL(request.url);
    const fileKey = url.searchParams.get("file");

    if (!fileKey) {
      return new Response("Missing file parameter", { status: 400 });
    }

    // Retrieve file object from Cloudflare R2
    const object = await env.BUG_REPORTS_BUCKET.get(fileKey);

    if (!object) {
      return new Response("File not found in storage", { status: 404 });
    }

    // Prepare response headers
    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set("etag", object.httpEtag);
    headers.set("Content-Disposition", `attachment; filename="${fileKey.substring(fileKey.indexOf("_", 4) + 1)}"` );

    // Return the R2 object body
    return new Response(object.body, {
      headers
    });

  } catch (error) {
    return new Response(`Error retrieving file: ${error.message}`, { status: 500 });
  }
}
