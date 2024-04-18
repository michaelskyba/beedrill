import { writable } from "svelte/store";

function getCookie(name) {
	const parts = `; ${document.cookie}`.split(`; ${name}=`);

	if (parts.length != 2)
		return;

	const cookie = parts.pop().split(';').shift();
	return decodeURIComponent(cookie);
}

function setCookie(name, value) {
	const days = 30;
	const expires = new Date(Date.now() + days * 864e5).toUTCString();
	document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}

function createCookieStore(key, initialValue) {
	const cookieValue = getCookie(key);
	const store = writable(cookieValue ? JSON.parse(cookieValue) : initialValue);

	store.subscribe(value => {
		setCookie(key, JSON.stringify(value));
	});

	return store;
}

export let user = createCookieStore("user", null);
export let page = createCookieStore("page", "home");
