import { apiRequest } from "./api.js";

document.getElementById("registerBtn").onclick = async () => {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const display_name = document.getElementById("display_name").value.trim();
    const bio = document.getElementById("bio").value.trim();
    const msg = document.getElementById("msg");

    try {
        //register
        await apiRequest("/users", "POST", {
            username,
            password,
            display_name,
            bio
        });

        msg.innerText = "Success! Redirecting to login...";
        setTimeout(() => window.location.href = "index.html", 1500);

    } catch (err) {
        msg.innerText = "Registration failed: " + err.message;
    }
};
