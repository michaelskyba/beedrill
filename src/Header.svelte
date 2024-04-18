<script>
	import Link from "./Link.svelte";
	import Logout from "./Logout.svelte";

	import { user, page, reviewState } from "./store.js";

	const titles = {
		"home": "🐝 Beedrill",
		"login": "⬇️ Login",
		"register": "⬆️ Register",
		"browse_decks": "🌎 Browse Public Decks",
		"my_decks": "📚 Personal Decks",
		"edit_deck": "✏️ Edit Deck",
		"review": "♻️ Review Cards",
	}
</script>

<h1>{titles[$page]}</h1>
<p>Welcome to 🐝 Beedrill, your smart companion for efficient learning!</p>

<Link
	pageLinked="home"
	text="Home"
/>

{#if !$user}
	<Link
		pageLinked="login"
		text="Login"
	/>
	<Link
		pageLinked="register"
		text="Register"
	/>
{:else}
	<Link
		pageLinked="browse_decks"
		text="Browse"
	/>
	<Link
		pageLinked="my_decks"
		text="My Decks"
	/>
	{#if $reviewState.card}
		<Link
			pageLinked="review"
			text="Review"
		/>
	{:else}
		<Link
			pageLinked="review"
			text="Review"
			disabled=true
		/>
	{/if}
	<Logout />
{/if}

<hr>

<style>
	hr {
		margin-bottom: 2em;
	}
</style>
