/* eslint-disable react/prop-types */
// @mui material components
import PlaylistsApi from "../../../api/playlists";

const PlaylistTable = () => {
  PlaylistsApi.GetList()
    .then((data) => {
      console.log(typeof data);
      return {
        columns: [
          { name: "Title", align: "left" },
          { name: "Duration", align: "center" },
          { name: "Track Count", align: "left" },
          { name: "Artwork Url", align: "left" },
          { name: "Permalink Url", align: "center" },
          { name: "sc_playlist_id", align: "center" },
        ],
        rows: data,
      };
    })
    .catch((error) => {
      console.error("Error fetching playlist data:", error);
    });
};

export default PlaylistTable;
