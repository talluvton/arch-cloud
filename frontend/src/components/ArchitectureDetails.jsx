const ArchitectureDetails = ({ architecture }) => {
  return (
    <div className="architecture-details">
      <h2>{architecture.title}</h2>
      <p><strong>Source:</strong> {architecture.source}</p>
      <p><strong>Provider:</strong> {architecture.provider}</p>
      <p><strong>Services:</strong></p>
      <ul>
        {(architecture.services ?? []).map((s, i) => (
          <li key={i}>{s.name} ({s.role})</li>
        ))}
      </ul>

      <p><strong>Flow:</strong></p>
      <ul>
        {(architecture.flow ?? []).map((f, i) => (
          <li key={i}>{f}</li>
        ))}
      </ul>

      <p><strong>Features:</strong></p>
      <ul>
        {(architecture.features ?? []).map((feat, i) => (
          <li key={i}>{feat}</li>
        ))}
      </ul>
      <p><strong>Scraped at:</strong> {architecture.timestamp}</p>
    </div>
  );
};

export default ArchitectureDetails;