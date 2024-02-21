import axios from "./index";
import { useAuth } from "../auth-context/auth.context";

class PlaylistsApi {
  static GetList = async () => {
    try {
      const { user } = useAuth();
      const response = await axios.get(`${base}`, { headers: { Authorization: `${user.token}` } });
      return response.data;
    } catch (error) {
      console.log(error);
    }
  };
}

let base = "playlists";

export default PlaylistsApi;
