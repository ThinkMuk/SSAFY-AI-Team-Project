import apiClient from "./client";

export function fetchPosts(placeId, { page = 1, size = 20 } = {}) {
  return apiClient
    .get(`/places/${placeId}/posts`, { params: { page, size } })
    .then((res) => res.data);
}

export function fetchPost(placeId, postId) {
  return apiClient
    .get(`/places/${placeId}/posts/${postId}`)
    .then((res) => res.data);
}

export function createPost(placeId, { nickname, password, title, content }) {
  return apiClient
    .post(`/places/${placeId}/posts`, { nickname, password, title, content })
    .then((res) => res.data);
}

export function updatePost(placeId, postId, { password, title, content }) {
  return apiClient
    .put(`/places/${placeId}/posts/${postId}`, { password, title, content })
    .then((res) => res.data);
}

export function deletePost(placeId, postId, { password }) {
  return apiClient
    .delete(`/places/${placeId}/posts/${postId}`, { data: { password } })
    .then((res) => res.data);
}
