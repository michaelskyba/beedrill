<script>
	import Header from "./Header.svelte";
	import Home from "./Home.svelte";
	import UserAuth from "./UserAuth.svelte";

	const user = null;
	const page = "home";
</script>

<Header />

{#if page == "home"}
	<Home />
{/if}

{#if !user}
	<UserAuth {page} />
{/if}
