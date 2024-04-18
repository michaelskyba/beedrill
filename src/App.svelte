<script>
	import Header from "./Header.svelte";
	import Home from "./Home.svelte";
	import Auth from "./Auth.svelte";

	import "./css/main.css"

	import { user, page } from "./store.js";
</script>

<Header />

{#if $page == "home"}
	<Home />
{:else if $page == "login" || $page == "register"}
	<Auth />
{/if}
