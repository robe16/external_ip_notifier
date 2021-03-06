echo "Running Build ID: ${env.BUILD_ID}"

String commit_id
String build_args
String deployLogin
String docker_img_name
def docker_img

node {

    deleteDir()

    stage("parameters") {
        // Parameters passed through from the Jenkins Pipeline configuration
        string(defaultValue: 'https://github.com/robe16/external_ip_notifier.git', description: 'GitHub URL for checking out project', name: 'githubUrl')
        string(defaultValue: 'external_ip_notifier', description: 'Name of application for Docker image and container', name: 'appName')
        string(defaultValue: '*', description: 'Server to deploy the Docker container', name: 'deploymentServer')
        string(defaultValue: '22', description: 'Server port for SSH connections', name: 'deploymentSSHport')
        string(defaultValue: '*', description: 'Username for the server the Docker container will be deployed to (used for ssh/scp)', name: 'deploymentUsername')
        string(defaultValue: '~/logs/external_ip_notifier.log', description: 'Location of log file on host device', name: 'fileLog')
        string(defaultValue: '~/config/external_ip_notifier/config_email.json', description: 'Location of config json file on host device', name: 'fileConfigEmail')
        string(defaultValue: '~/config/external_ip_notifier/ip.txt', description: 'Location of file where last IP address is saved', name: 'fileLastip')
        //
        docker_volumes = ["-v ${params.fileLog}:/external_ip_notifier/log/external_ip_notifier.log",
                          "-v ${params.fileConfigEmail}:/external_ip_notifier/notify/config_email.json",
                          "-v ${params.fileLastip}:/external_ip_notifier/ip/last_ip.txt"].join(" ")
        //
        deployLogin = "${params.deploymentUsername}@${params.deploymentServer}"
        //
    }

    if (params["deploymentServer"]!="*" && params["deploymentUsername"]!="*" && params["serverIp"]!="*") {

        stage("checkout") {
            git url: "${params.githubUrl}"
            sh "git rev-parse HEAD > .git/commit-id"
            commit_id = readFile('.git/commit-id').trim()
            echo "Git commit ID: ${commit_id}"
        }

        docker_img_name_commit = "${params.appName}:${commit_id}"
        docker_img_name_latest = "${params.appName}:latest"

        stage("build") {
            try {sh "docker image rm ${docker_img_name_latest}"} catch (error) {}
            sh "docker build -t ${docker_img_name_commit} ."
            sh "docker tag ${docker_img_name_commit} ${docker_img_name_latest}"
        }

        stage("deploy"){
            //
            String docker_img_tar = "docker_img.tar"
            //
            try {
                // remove any old tar files from cicd server
                sh "rm ~/${docker_img_tar}"
            } catch(error) {
                echo "No ${docker_img_tar} file to remove."
            }
            // create tar file of image
            sh "docker save -o ~/${docker_img_tar} ${docker_img_name_commit}"
            // xfer tar to deploy server
            sh "scp -v -o StrictHostKeyChecking=no -P ${deploymentSSHport} ~/${docker_img_tar} ${deployLogin}:~"
            // load tar into deploy server registry
            sh "ssh -o StrictHostKeyChecking=no ${deployLogin} -p ${deploymentSSHport} \"docker load -i ~/${docker_img_tar}\""
            // remove the tar file from deploy server
            sh "ssh -o StrictHostKeyChecking=no ${deployLogin} -p ${deploymentSSHport} \"rm ~/${docker_img_tar}\""
            // remove the tar file from cicd server
            sh "rm ~/${docker_img_tar}"
            // Set 'latest' tag to most recently created docker image
            sh "ssh -o StrictHostKeyChecking=no ${deployLogin} -p ${deploymentSSHport} \"docker tag ${docker_img_name_commit} ${docker_img_name_latest}\""
            //
        }

        stage("start container"){
            // Stop existing container if running
            sh "ssh ${deployLogin} \"docker rm -f ${params.appName} && echo \"container ${params.appName} removed\" || echo \"container ${params.appName} does not exist\"\""
            // Start new container
            sh "ssh ${deployLogin} \"docker run --restart unless-stopped -d ${docker_volumes} --name ${params.appName} ${docker_img_name_latest}\""
        }

    } else {
        echo "Build cancelled as required parameter values not provided by pipeline configuration"
    }

}