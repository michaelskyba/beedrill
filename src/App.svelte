<script>
	import Header from "./Header.svelte";
	import Home from "./Home.svelte";
	import Auth from "./Auth.svelte";
	import MyDecks from "./MyDecks.svelte";
	import BrowseDecks from "./BrowseDecks.svelte";
	import Review from "./Review.svelte";

	import "./css/sakura.css"
	import "./css/main.css"

	import { user, page } from "./store.js";
</script>

<Header />

{#if $page == "home"}
	<Home />
{:else if $page == "login" || $page == "register"}
	<Auth />
{:else if $page == "my_decks"}
	<MyDecks />
{:else if $page == "browse_decks"}
	<BrowseDecks />
{:else if $page == "review"}
	<Review />
{/if}
