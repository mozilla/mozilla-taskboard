class custom {
    case $operatingsystem {
        ubuntu: {
            package {
                ["vim", "git-core", "screen", "byobu", "ack-grep"]:
                    ensure => installed;
            }
        }
    }
}
