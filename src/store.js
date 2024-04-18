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
export let myDecks = createCookieStore("myDecks", [
	{
		id: 1,
		name: "Foo",
		due_cards: 12,
	},
	{
		id: 2,
		name: "Baz",
		due_cards: 0,
	},
	{
		id: 3,
		name: "1713442506",
		due_cards: 5,
	},
	{
		id: 4,
		name: "Bar",
		due_cards: 2,
	},
	{
		id: 5,
		name: "Second Last",
		due_cards: 0,
	},
	{
		id: 6,
		name: "Last",
		due_cards: 1,
	},
]);

/*
int: deck_id
*/
export let reviewDeck = createCookieStore("reviewDeck", 1)

/*
Array of objects
{
	id: int
	name: string
	author: string
	cards: int
}
*/
export let publicDecks = createCookieStore("publicDecks", [
	{
		id: 7,
		name: "Godhead",
		author: "Mira",
		cards: 45
	},
	{
		id: 8,
		name: "Tensor",
		author: "George",
		cards: 4
	},
])
