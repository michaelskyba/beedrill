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
Array of deck objects
{
	id: int
	mine: bool (whether the user owns them)
	name: string
	author: string
	due_cards: int
}
*/
export let decks = createCookieStore("decks", [
	{
		id: 1,
		mine: true,
		name: "Foo",
		author: "Joshua",
		due_cards: 12,
	},
	{
		id: 2,
		mine: true,
		name: "Baz",
		author: "Michael",
		due_cards: 0,
	},
]);
