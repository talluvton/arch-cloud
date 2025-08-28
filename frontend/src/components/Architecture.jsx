import ArchitectureDetails from "./ArchitectureDetails";

const Architecture = ({ architecture }) => {
  return (
    <li className="architecture">
      <ArchitectureDetails architecture={architecture} />
    </li>
  );
};

export default Architecture;