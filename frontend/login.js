import { apiRequest } from "./api.js";

document.getElementById("loginBtn").onclick = async () => {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const msg = document.getElementById("msg");

    // need to make token first login
    //localhost/api/users/token 
    try {
        const data = await apiRequest("/auth/login", "POST", {
            username,
            password
        });

        localStorage.setItem("token", data.access_token);
        window.location.href = "feed.html";
    } catch (err) {
        msg.innerText = "Login failed: " + err.message;
    }
};
