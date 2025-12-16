import { apiRequest } from "./api.js";

const feedContainer = document.getElementById("feed");

const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");

document.getElementById("logoutBtn").onclick = () => {
    localStorage.removeItem("token");
    window.location.href = "index.html";
};

// optional
imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];
    imagePreview.innerHTML = "";

    if (file) {
        const reader = new FileReader();
        reader.onload = e => {
            const img = document.createElement("img");
            img.src = e.target.result;
            imagePreview.appendChild(img);
        };
        reader.readAsDataURL(file);
    }
});


// add optional image 
document.getElementById("createPostBtn").onclick = async () => {
    const caption = document.getElementById("caption").value;

    // check
    const formData = new FormData();

    if (!caption && !imageInput.files[0]) {
        alert("Write something or add an image!");
        return;
    }

    if (imageInput.files[0]) {
        formData.append("file", imageInput.files[0]);
    }



    // if (!caption.trim()) return alert("Caption required!");

    console.log("here is what user said", caption);
    // console.log("here is what user said", imageInput.files[0]);

    formData.append("caption", caption);

    await apiRequest("/posts", "POST", formData, true);
    loadFeed();
};

async function loadFeed() {
    feedContainer.innerHTML = "";

    try {
        const posts = await apiRequest("/posts/feed", "GET", null, true);

        posts.forEach(post => {
            const div = document.createElement("div");
            div.className = "post";

            const imageHtml = post.id // should be changed
            ? `<img src="http://localhost:8000/api/posts/${post.id}/image" alt="Post image" loading="lazy" />` : "";

            div.innerHTML = `
                <p><strong>@${post.username}</strong></p>
                <p>${post.caption}</p>
                ${imageHtml}
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

// image upload
// async function uploadPost(files) {
//     const formData = new FormData();
//     files.forEach(file => formData.append("files", file));

//     await apiRequest("/posts/upload", "POST", formData, true);
//     loadFeed();
// }



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
