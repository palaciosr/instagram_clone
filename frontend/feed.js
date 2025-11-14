import { apiRequest } from "./api.js";

const feedContainer = document.getElementById("feed");

document.getElementById("logoutBtn").onclick = () => {
    localStorage.removeItem("token");
    window.location.href = "index.html";
};

document.getElementById("createPostBtn").onclick = async () => {
    const caption = document.getElementById("caption").value;

    // if (!caption.trim()) return alert("Caption required!");

    console.log("here is what user said", caption);

    await apiRequest("/posts", "POST", { caption }, true);
    loadFeed();
};

async function loadFeed() {
    feedContainer.innerHTML = "";

    try {
        const posts = await apiRequest("/posts/feed", "GET", null, true);

        posts.forEach(post => {
            const div = document.createElement("div");
            div.className = "post";

            div.innerHTML = `
                <p><strong>@${post.username}</strong></p>
                <p>${post.caption}</p>
                <button class="likeBtn" data-id="${post.id}">
                    Like (${post.likes})
                </button>

                <div>
                    <input class="commentInput" data-id="${post.id}" placeholder="Comment..." />
                    <button class="commentBtn" data-id="${post.id}">
                        Send
                    </button>
                </div>

                <div class="comments">
                    ${post.comments.map(c => `<p><strong>${c.username}</strong>: ${c.text}</p>`).join("")}
                </div>
            `;

            feedContainer.appendChild(div);
        });

        // Buttons Handlers
        document.querySelectorAll(".likeBtn").forEach(btn =>
            btn.onclick = () => likePost(btn.dataset.id)
        );

        document.querySelectorAll(".commentBtn").forEach(btn =>
            btn.onclick = () => commentPost(btn.dataset.id)
        );

    } catch (err) {
        console.error(err);
        feedContainer.innerHTML = "<p>Error loading feed</p>";
    }
}

async function likePost(id) {
    await apiRequest(`/posts/${id}/like`, "POST", {}, true);
    loadFeed();
}

async function commentPost(id) {
    const input = document.querySelector(`.commentInput[data-id="${id}"]`);
    const text = input.value;

    if (!text.trim()) return;

    await apiRequest(`/posts/${id}/comment`, "POST", { text }, true);
    loadFeed();
}

loadFeed();
