const API_BASE = "http://localhost:8000/api";

export async function apiRequest(path, method = "GET", body = null, auth = false) {
    // const headers = { "Content-Type": "application/json" };

    const headers = {};

    // Only add Content-Type if we're sending JSON (not FormData)
    const isFormData = body instanceof FormData;
    if (!isFormData && body !== null) {
        headers["Content-Type"] = "application/json";
    }


    if (auth) {
        const token = localStorage.getItem("token");
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }else{
            console.warn("No auth token found");
        }

    }

    const res = await fetch(API_BASE + path, {
        method,
        headers,
        body: isFormData ? body : (body ? JSON.stringify(body) : null),
    });

    if (!res.ok) {
        const error = await res.text();
        throw new Error(`HTTP ${res.status}: ${error}`);
    }

    const contentType = res.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
        return await res.json();
    }
    return await res.text();


}
