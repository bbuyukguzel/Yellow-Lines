<template>
    <div>
        <v-navigation-drawer clipped fixed v-model="drawer" app>
            <v-list dense>
                <v-list-tile to="/">
                    <v-list-tile-action>
                        <v-icon>home</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>Homepage</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
                <v-list-tile to="/dashboard">
                    <v-list-tile-action>
                        <v-icon>dashboard</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>Dashboard</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
                <v-list-tile to="/test">
                    <v-list-tile-action>
                        <v-icon>settings</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>Settings</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>

                <li v-if="!isAuthenticated">
                    <a href="#" @click.prevent="login">Login</a>
                </li>
                <li v-if="isAuthenticated">
                    <a href="#" @click.prevent="logout">Log out</a>
                </li>

            </v-list>
        </v-navigation-drawer>
        <v-toolbar app fixed clipped-left>
            <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
            <v-toolbar-title>Yellow Lines</v-toolbar-title>
        </v-toolbar>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                drawer: false,
                isAuthenticated: false
            }
        },
        async created() {
            try {
                await this.$auth.renewTokens();
            } catch (e) {
                console.log(e);
            }
        },
        methods: {
            login() {
                this.$auth.login();
            },
            logout() {
                this.$auth.logOut();
            },
            handleLoginEvent(data) {
                this.isAuthenticated = data.loggedIn;
                this.profile = data.profile;
            }
        }
    }
</script>

<style scoped>

</style>
