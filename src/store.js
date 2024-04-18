import { writable, get } from "svelte/store";

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

export let page = createCookieStore("page", "home");

/*
{
	user_id: int
	username: string
}
*/
export let user = createCookieStore("user", null);

/*
Array of objects
{
	id: int
	name: string
	due_cards: int
}
*/
export let myDecks = createCookieStore("myDecks", []);

/*
deck_id: int
due_card_count: int
step: "front" | "back"
card: null | {
	id: int,
	front: string,
	back: string
}
*/
export let reviewState = createCookieStore("reviewState", {
	deck_id: 0,
	deck_name: "",
	due_card_count: 0,
	step: "front",
	card: null,
});

/*
id: int
name: string
*/
export let editingDeck = createCookieStore("editingDeck", {
	id: 0,
	name: "",
});

/*
Array of objects
{
	id: int
	name: string
	author: string
	card_count: int
}
*/
export let publicDecks = createCookieStore("publicDecks", []);
