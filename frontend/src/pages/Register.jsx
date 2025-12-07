import Form from "../components/Form/Form";
import PageContainer from "../components/PageContainer/PageContainer";

const Register = () => {
  return (
    <PageContainer>
      <Form route={"/api/user/register/"} method={"register"} />
    </PageContainer>
  );
};

export default Register;
