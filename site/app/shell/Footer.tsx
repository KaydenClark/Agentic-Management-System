// Keep build identity on-site. AMS_COMMIT_SHA is fixed by next.config.ts.

export function Footer() {
  const sha = process.env.AMS_COMMIT_SHA || "unknown";
  const known = /^[0-9a-f]{7,40}$/.test(sha);
  return (
    <footer className="site-footer">
      <div className="container site-footer-inner">
        <span>Built from commit</span>
        {known ? (
          <span className="mono" data-commit-sha={sha} title={sha}>
            {sha.slice(0, 7)}
          </span>
        ) : (
          <span className="mono" data-commit-sha={sha}>
            {sha}
          </span>
        )}
      </div>
    </footer>
  );
}
