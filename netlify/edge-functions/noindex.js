// Noindex ONLY the staging *.netlify.app preview — never the real domain.
// When drsharongam.com is pointed here later, it will NOT be noindexed.
export default async (request, context) => {
  const res = await context.next();
  try {
    const host = new URL(request.url).hostname;
    if (host.endsWith(".netlify.app")) {
      res.headers.set("X-Robots-Tag", "noindex, nofollow");
    }
  } catch (e) {}
  return res;
};
