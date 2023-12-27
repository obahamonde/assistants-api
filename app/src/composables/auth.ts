import useStore from "~/store";

export const useAuth = () => {
  const loginWithRedirect = async () => {
    const response = await fetch("/api/auth/authorize", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    const { url } = data;
    window.open(url, "_self");
  };
  const { query } = useRoute();

  onMounted(async () => {
    const code = query.code;
    if (code) {
      const { state } = useStore();
      const response = await fetch("/api/auth/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code }),
      });
      const data = await response.json();
      const { token, user_info } = data;
      state.token = token;
      state.user = user_info;
    }
  });
  return { loginWithRedirect };
};
