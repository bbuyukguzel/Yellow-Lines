<template>
    <v-app id="inspire" dark>
        <navigation-component ref="ref_nav"></navigation-component>

        <v-content>
            <v-container fluid fill-height>
                <v-layout justify-center align-center>
                    <v-flex shrink>
                        <v-tabs centered color="cyan" dark icons-and-text>
                            <v-tabs-slider color="yellow"></v-tabs-slider>

                            <v-tab> Register</v-tab>
                            <v-tab> Login</v-tab>

                            <v-tab-item>
                                <v-card flat>
                                    <v-card-text>

                                        <form>
                                            <v-text-field
                                                    v-model="email"
                                                    :error-messages="emailErrors"
                                                    label="E-mail"
                                                    required
                                                    @input="$v.email.$touch()"
                                                    @blur="$v.email.$touch()"
                                            ></v-text-field>
                                            <v-text-field
                                                    v-model="password"
                                                    :error-messages="passwordErrors"
                                                    :counter="10"
                                                    label="Password"
                                                    required
                                                    @input="$v.password.$touch()"
                                                    @blur="$v.password.$touch()"
                                            ></v-text-field>

                                            <v-btn @click="handleRegister">submit</v-btn>
                                            <v-btn @click="clear">clear</v-btn>
                                        </form>

                                    </v-card-text>
                                </v-card>
                            </v-tab-item>

                            <v-tab-item>
                                <v-card flat>
                                    <v-card-text>

                                        <form>
                                            <v-text-field
                                                    v-model="email"
                                                    :error-messages="emailErrors"
                                                    label="E-mail"
                                                    required
                                                    @input="$v.email.$touch()"
                                                    @blur="$v.email.$touch()"
                                            ></v-text-field>
                                            <v-text-field
                                                    v-model="password"
                                                    :error-messages="passwordErrors"
                                                    :counter="10"
                                                    label="Password"
                                                    required
                                                    @input="$v.password.$touch()"
                                                    @blur="$v.password.$touch()"
                                            ></v-text-field>

                                            <v-btn @click="handleLogin">submit</v-btn>
                                        </form>

                                    </v-card-text>
                                </v-card>
                            </v-tab-item>
                        </v-tabs>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-content>
        <footer-component/>
    </v-app>
</template>

<script>
    import axios from 'axios'
    import {required, email} from 'vuelidate/lib/validators'
    import Navigation from "@/components/Navigation";
    import Footer from "@/components/Footer";

    export default {
        components: {
            'navigation-component': Navigation,
            'footer-component': Footer,
        },
        validations: {
            email: {required, email: email},
            password: {required},
        },
        data() {
            return {
                email: '',
                password: '',
                invalidCredentials: false,
            }
        },
        methods: {
            submit() {
                this.$v.$touch()
            },
            clear() {
                this.$v.$reset()
                this.email = ''
                this.password = ''
            },
            handleRegister() {
                axios.post('/api/v1/register', {
                    'email': this.email,
                    'password': this.password
                })
                    .then((response) => {
                        // server return something
                        console.log(response.data)
                    })
                    .catch((error) => {
                        // TODO: action for exceptions?
                        /* eslint-disable no-console */
                        console.log(error);
                        /* eslint-enable no-console */
                    })
            },
            handleLogin() {
                let formData = {
                    email: this.email,
                    password: this.password,
                }

                this.$store.dispatch('auth/login', formData).then(() => {
                    this.$router.push('/dashboard');
                });
            }
        },
        computed: {
            passwordErrors() {
                const errors = []
                if (!this.$v.password.$dirty) return errors
                !this.$v.password.required && errors.push('Password is required.')
                return errors
            },
            emailErrors() {
                const errors = []
                if (!this.$v.email.$dirty) return errors
                !this.$v.email.email && errors.push('Must be valid e-mail')
                !this.$v.email.required && errors.push('E-mail is required')
                return errors
            }
        }
    }
</script>
