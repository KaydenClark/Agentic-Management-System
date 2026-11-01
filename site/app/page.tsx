export default function Home() {
  return (
    <>
      <p className="eyebrow">Start here</p>
      <h1>Agentic Management System</h1>
      <p className="lede" data-opener="">
        The Agentic Management System, or AMS, is how Kayden runs AI assistants, called agents, on real
        projects. Each piece of work starts as a written request, is split into small tasks, and is checked
        before it counts as done, so anyone can see what was asked, who did it and what proof there is.
      </p>
      <section className="card" aria-labelledby="this-site">
        <h2 id="this-site">This site</h2>
        <p>
          The AMS is building this site, and the site shows the real records rather than describing them. The
          tour pages arrive one reviewed change at a time. The footer of every page names the exact commit it
          was built from, linked to the code on GitHub.
        </p>
      </section>
    </>
  );
}
