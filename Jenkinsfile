node("dev") {
    checkout scm

    if (env.BRANCH_NAME == 'master' || env.TAG_NAME != null) {
        //withEnv(["DOCKER_HOST=tcp://127.0.0.1:2376"]) {

            /* prepare environment */
            def tag_name = env.TAG_NAME

            if(tag_name == null){
                tag_name = gitTagName()
            }

            if(tag_name){}
            else{
                tag_name = 'latest'
            }

            // in future execute a loop within each Jenkins pipeline stage
            def site = 'nau'
            def dockerRegistryOrganization = 'nauedu'
            def dockerImageName = 'richie-site-nau'

            stage('Generate version.json file') {
                def gitUrl = sh(returnStdout: true, script: 'git config remote.origin.url').trim()
                def gitCommit = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()

                // Create a version.json à-la-mozilla
                // https://github.com/mozilla-services/Dockerflow/blob/master/docs/version_object.md
                sh ("printf '{\"commit\":\"%s\",\"version\":\"%s\",\"source\":\"%s\",\"build\":\"%s\"}\n' \"$gitCommit\" \"$tag_name\" \"$gitUrl\" \"$env.BUILD_URL\" > sites/$site/version.json")
            }

            stage('Build docker images') {
                //   final foundSitesFolders = findFiles(glob: 'sites/*')
                //   makeBuildForAllSites(foundSitesFolders)

                sh "export RICHIE_SITE=${site} && make env.d/aws && make build"
            }
            stage('Check built image availability') {
                sh "docker images 'nau:development'"
                sh "docker images 'nau:production'"
                //sh "docker images 'nau-nginx:production'"
            }

            stage('Check version.json file') {
                sh "make ci-version"
            }

            stage('Run Django migrations') {
                sh "make ci-migrate"
            }

            stage('Run Django checks with production image') {
                sh "make ci-check"
            }

            stage('Check that the changelog, versions and tag are always in sync') {
                sh "bin/ci check_tag ${site} ${tag_name}"
            }

            stage('Tag app image') {
                sh "docker tag ${site}:production ${dockerRegistryOrganization}/${dockerImageName}:${tag_name}"
            }
            stage('Login to DockerHub') {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-registry-credentials', passwordVariable: 'DOCKER_REGISTRY_PWD', usernameVariable: 'DOCKER_REGISTRY_USER')]) {
                    sh "echo '\$DOCKER_REGISTRY_PWD' | docker login -u '\$DOCKER_REGISTRY_USER' --password-stdin"
                }
            }
            stage('Publish app image to docker registry') {
                sh "docker push ${dockerRegistryOrganization}/${dockerImageName}:${tag_name}"
            }
        //}
    }

    stage('Cleanup') {
        cleanWs notFailBuild: true
    }
}

String gitTagName() {
    commit = getCommit()
    if (commit) {
      try{
        desc = sh(script: "git describe --tags ${commit}", returnStdout: true)?.trim()
        if (isTag(desc)) {
            return desc
        }
      }catch (err) {
        echo "Unable to get tag"
      }
    }
    return null
}

String getCommit() {
    return sh(script: 'git rev-parse HEAD', returnStdout: true)?.trim()
}

boolean getTags(String branch){
    sh(script: "git pull origin ${branch} --tag")
    return true
}

@NonCPS
boolean isTag(String desc) {
    match = desc =~ /.+-[0-9]+-g[0-9A-Fa-f]{6,}$/
    result = !match
    match = null // prevent serialisation
    return result
}

@NonCPS // has to be NonCPS or the build breaks on the call to .each
def makeBuildForAllSites(sitesDirectories) {
    sitesDirectories.each { siteDir ->
        if (siteDir.directory) {
            sh "export RICHIE_SITE=${siteDir.name} && make build"
        }
    }
}
