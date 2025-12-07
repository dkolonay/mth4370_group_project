import Navbar from "../Navbar/Navbar";

import "./PageContainer.css";

const PageContainer = ({ children }) => {
  return (
    <div className={"page-container"}>
      <Navbar />
      {children}
    </div>
  );
};

export default PageContainer;
