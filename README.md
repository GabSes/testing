This is one task that is divided into several smaller parts.

For these tasks use python 3

You will need a router with sim card and wireless connection.

Your first task is to create a program which will create authentication using the correct API endpoint. With that authentication you need to send an API request to create an event reporting rule to send a SMS message when wifi config changes happen. The project should have a JSON configuration file that has events reporting rule’s configuration in it and has router information needed to send API requests.

Second task is to create a program that will connect to a router over SSH protocol. When connected it should make changes to wireless access point. All the changes must also be visible in WEB‘UI. The project should have a configuration file that has router information for SSH connection and the access point configuration. After applying changes you must verify that’s changes did apply correctly.


