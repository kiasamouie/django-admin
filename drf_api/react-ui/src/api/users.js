import axios from "./index";
import { useAuth } from "../auth-context/auth.context";

class UsersApi {
  static GetList = () => {
    const { user } = useAuth();
    return axios.get(`${base}`, { headers: { Authorization: `${user.token}` } });
  };
}

let base = "users";

export default UsersApi;
