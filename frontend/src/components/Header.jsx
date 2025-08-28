const Header = ({ showForm, setShowForm }) => {
  const appTitle = "Cloud Architecture";
  return (
    <header className="header">
      <div className="title">
        <img src="cloud_logo.png" height="68" width="68" alt="Cloud Logo" />
        <h1>{appTitle}</h1>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', alignItems: 'flex-end' }}>
        <button
          className="btn btn-large btn-open"
          onClick={() => setShowForm((show) => !show)}
        >
          {showForm ? "Close" : "Scrape Cloud Architecture"}
        </button>
      </div>      
    </header>
  );
};

export default Header;