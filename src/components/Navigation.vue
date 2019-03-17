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
                <v-list-tile to="/newTask">
                    <v-list-tile-action>
                        <v-icon>add</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>Add New Task</v-list-tile-title>
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
            </v-list>
        </v-navigation-drawer>
        <v-toolbar app fixed clipped-left>
            <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
            <v-toolbar-title>Yellow Lines</v-toolbar-title>

            <v-spacer/>
            <v-toolbar-items>
                <v-btn v-if="!isAuthenticated" flat @click.prevent="login">
                    <v-icon left dark>person</v-icon>
                    Sign In
                </v-btn>
                <!-- only show if authenticated -->
                <v-btn v-if="isAuthenticated" to="/profile" flat>
                    <v-icon left dark>account_circle</v-icon>
                    Profile
                </v-btn>
                <v-btn v-if="isAuthenticated" flat @click.prevent="logout">
                    <v-icon left dark>exit_to_app</v-icon>
                    Sign Out
                </v-btn>
            </v-toolbar-items>

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
