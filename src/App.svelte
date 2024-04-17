<script>
	import Header from "./Header.svelte";
	import Home from "./Home.svelte";
	import UserAuth from "./UserAuth.svelte";

	import { user, page } from "./store.js";

	// user.update(u => 1)
</script>

<Header />

{#if $page == "home"}
	<Home />
{/if}

{#if !user}
	<UserAuth />
{/if}
