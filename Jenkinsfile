elifePipeline {
    def commit
    DockerImage image
    stage 'Checkout', {
        checkout scm
        commit = elifeGitRevision()
    }

    node('containers-jenkins-plugin') {
        stage 'Build images', {
            checkout scm
            dockerComposeBuild(commit)
        }

        stage 'Project tests', {
            dockerComposeProjectTests('digests', commit, ['/srv/digests/build/*.xml'])
            dockerComposeSmokeTests(commit, [
                'scripts': [
                    'wsgi': './smoke_tests_wsgi.sh',
                ],
            ])
        }

        elifeMainlineOnly {
            stage 'Push image', {
                image = DockerImage.elifesciences(this, "digests", commit)
                image.push()
            }
        }
    }


    elifeMainlineOnly {
        stage 'Approval', {
            elifeGitMoveToBranch commit, 'approved'
            node('containers-jenkins-plugin') {
                image = DockerImage.elifesciences(this, "digests", commit)
                image.pull()
                image.tag('approved').push()
                image.tag('latest').push()
            }
        }
    }
}

