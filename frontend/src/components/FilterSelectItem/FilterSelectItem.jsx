import "./FilterSelectItem.css"

const FilterSelectItem = ({ name, selected, toggle }) => {
  return (
    <li className={`filter-select-item ${selected ? "filter-selected" : ""}`} onClick={()=>{toggle(name)}}>
      <p>{name}</p>
    </li>
  );
};

export default FilterSelectItem;
