<script>
	import Link from "./Link.svelte";

	import { user } from "./store.js";
</script>

<h1>Beedrill</h1>

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
