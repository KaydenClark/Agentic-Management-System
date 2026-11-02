// Footer on every page: the commit this build was made from, linked to it on
// GitHub. AMS_COMMIT_SHA is fixed at build time by next.config.ts.
const REPO = "https://github.com/KaydenClark/Agentic-Management-System";

export function Footer() {
  const sha = process.env.AMS_COMMIT_SHA || "unknown";
  const known = /^[0-9a-f]{7,40}$/.test(sha);
  return (
    <footer className="site-footer">
      <div className="container site-footer-inner">
        <span>Built from commit</span>
        {known ? (
          <a className="mono" data-commit-sha={sha} href={`${REPO}/commit/${sha}`}>
            {sha.slice(0, 7)}
          </a>
        ) : (
          <span className="mono" data-commit-sha={sha}>
            {sha}
          </span>
        )}
      </div>
    </footer>
  );
}
