<template>
    <v-app id="inspire" dark>
        <navigation-component/>

        <v-content>
            <v-container fluid fill-height>
                <v-layout justify-center align-center>
                    <v-flex shrink>
                        <span>Dont't Panic [Homepage]</span>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-content>

        <footer-component/>
    </v-app>
</template>

<script>
    import Navigation from "@/components/Navigation";
    import Footer from "@/components/Footer";

    export default {
        name: "Homepage",
        components: {
            'navigation-component': Navigation,
            'footer-component' : Footer
        },
        data: () => ({}),
        props: {},
    }
</script>

<style scoped>

</style>
