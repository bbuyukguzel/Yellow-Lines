<template>
    <div class="and-or-template" :class="isFirst ? 'and-or-first' : '' ">
        <div class="and-or-top">
            <v-container fluid>
                <v-layout row>
                    <v-flex grow class="text-sm-left pa-0">
                        <v-chip small label :color=" isAnd ? 'deep-purple lighten-1' : 'deep-purple lighten-4' "
                                @click.prevent="clickAnd">And
                        </v-chip>
                        <v-chip small label :color=" !isAnd ? 'deep-purple lighten-1' : 'deep-purple lighten-4' "
                                @click.prevent="clickOr">Or
                        </v-chip>
                    </v-flex>
                    <v-flex grow class="text-sm-right pa-0">
                        <v-chip small label color="deep-purple lighten-1" @click.prevent="addRule">
                            +add
                        </v-chip>
                        <v-chip small label color="deep-purple lighten-1" @click.prevent="addGroup">
                            +add(group)
                        </v-chip>
                        <v-chip v-if="!isFirst" small label color="deep-purple lighten-1" @click.prevent="deleteSelf()">
                            delete
                        </v-chip>
                    </v-flex>
                </v-layout>

                <v-layout row>
                    <v-flex>
                        <rule
                                v-for="(rule, index) in rules" ref="rules"
                                :options="options" :key="rule" @delete-rule="deleteRule(index)">
                        </rule>
                        <and-or
                                class="and-or-offset"
                                v-for="(group, index) in groups" ref="groups"
                                :options="options" :key="group" @delete-group="deleteGroup(index)">
                        </and-or>
                    </v-flex>
                </v-layout>
            </v-container>
        </div>
    </div>
</template>

<script>
    import Rule from './Rule'

    export default {
        name: 'andOr',
        components: {
            Rule
        },
        props: {
            options: {
                type: Object,
                required: true
            },
            isFirst: {
                type: Boolean,
                default: false
            }
        },
        created() {
            this.addRule();
        },
        data() {
            return {
                isAnd: true,
                groups: [],
                rules: []
            }
        },
        methods: {
            clickAnd() {
                this.isAnd = true;
            },

            clickOr() {
                this.isAnd = false;
            },

            addRule() {
                var id = this.generateId();
                this.rules.push(id);
            },

            addGroup() {
                var id = this.generateId();
                this.groups.push(id);
            },

            deleteSelf() {
                this.$emit('delete-group');
            },

            deleteRule(index) {
                this.rules.splice(index, 1);
            },

            deleteGroup(index) {
                this.groups.splice(index, 1);
            },

            queryFormStatus() {
                var query = {};
                var rules = this.$refs.rules || {};
                var groups = this.$refs.groups || {};
                var i, j;

                query['condition'] = this.isAnd ? 'AND' : 'OR';
                query['rules'] = [];
                for (i = 0; i < rules.length; i++) {
                    query.rules.push(rules[i].queryFormStatus());
                }
                for (j = 0; j < groups.length; j++) {
                    query.rules[query.rules.length] = groups[j].queryFormStatus();
                }
                return query;
            },

            fillFormStatus(data) {
                var i, len;
                var group = this;
                group.rules = [];
                group.groups = [];
                if (data) {
                    group.isAnd = /and/i.test(data.condition);
                    len = data.rules.length;
                    for (i = 0; i < len; i++) {
                        if (data.rules[i].condition) {
                            group.groups.push(group.generateId());
                            (function (i, index) {
                                group.$nextTick(function () {
                                    group.$refs.groups[index].fillFormStatus(data.rules[i]);
                                });
                            })(i, group.groups.length - 1);
                        }
                        else {
                            group.rules.push(group.generateId());
                            (function (i, index) {
                                group.$nextTick(function () {
                                    group.$refs.rules[index].fillRuleStatus(data.rules[i]);
                                });
                            })(i, group.rules.length - 1);
                        }
                    }
                }
            },

            generateId() {
                return 'xxxxxxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
                    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
                    return v.toString(16);
                });
            }
        }
    }
</script>

<style>
    .and-or-template {
        position: relative;
        border-radius: 3px;
        border: 1px solid #6d77b8;
        border-top: 3px solid #d2d6de;
        margin-bottom: 20px; /* can be removed later */
        box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
        border-top-color: #6d77b8;
    }

    .and-or-template:before,
    .and-or-template:after {
        content: '';
        position: absolute;
        left: -26px;
        width: 16px;
        height: calc(50% + 18px);
        border-color: #c0c5e2;
        border-style: solid;
    }

    .and-or-template:before {
        top: -23px;
        border-width: 0 0 2px 2px;
    }

    .and-or-template:after {
        top: 50%;
        border-width: 0 0 0 2px;
    }

    .and-or-first:before,
    .and-or-first:after,
    .and-or-template:last-child:after {
        border: none;
    }

    .and-or-top {
        padding: 0;
    }

    .and-or-offset {
        margin-left: 30px; /* child box */
        margin-top: 40px;
    }
</style>
