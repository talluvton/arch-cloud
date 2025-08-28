import Architecture from "./Architecture";

const ArchitecturesList = ({ architectures }) => {
  if (architectures.length === 0)
    return <p className="message">No architectures scraped yet.</p>;

  return (
    <section>
      <ul className="architectures-list">
        {architectures.map((a) => {
          const key = a.id; 
          return <Architecture key={key} architecture={a} />;
        })}
      </ul>
    </section>
  );
};

export default ArchitecturesList;
