<script>
	import Header from "./Header.svelte";
	import Home from "./Home.svelte";
	import Register from "./Register.svelte";

	import "./css/main.css"

	import { user, page } from "./store.js";

	// user.update(u => 1)
</script>

<Header />

{#if $page == "home"}
	<Home />
{:else if $page == "login"}
	Login
{:else if $page == "register"}
	<Register />
{/if}
