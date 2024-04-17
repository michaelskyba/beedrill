<script>
	import Link from "./Link.svelte";

	import { user, page } from "./store.js";

	const titles = {
		"home": "Beedrill",
		"login": "Login",
		"register": "Register"
	}
</script>

<h1>{titles[$page]}</h1>

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
		pageLinked="browse"
		text="Browse"
	/>
	<Link
		pageLinked="my_decks"
		text="My Decks"
	/>
{/if}

<hr>

<style>
	hr {
		margin-bottom: 2em;
	}
</style>
