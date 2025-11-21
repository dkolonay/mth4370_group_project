import Form from "../components/Form/Form";
import PageContainer from "../components/PageContainer/PageContainer";

const Login = () => {
  return (
    <PageContainer>
      <Form route={"/api/token/"} method={"login"} />
    </PageContainer>
  );
};

export default Login;
