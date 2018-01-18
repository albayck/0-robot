from urllib.parse import urlparse


class TemplateUID:

    def __init__(self, host, account, repo, name, version):
        self.host = host
        self.account = account
        self.repo = repo
        self.name = name
        self.version = version

    @classmethod
    def parse(cls, uid):
        """
        Parse a template unique identifier.
        A tempate is identify by the url fo the git repository from where it comes from.
        There are different information extracted from
        - the host
        - the account
        - the repository name
        - the name of the template itself
        - a version
        e.g: https://github.com/account/repository/name/version would result into
        host: github.com
        account: account
        repository name: repository
        template name: name
        version: version
        """
        host, account, repo, name, version = None, None, None, None, None

        parsed = urlparse(uid)
        if parsed.netloc:
            host = parsed.netloc

        path = parsed.path.rstrip('/').lstrip('/')

        ss = path.split('/')

        if host is None and len(ss) == 5:
            host, account, repo, name, version = ss
        elif host is not None and len(ss) == 4:
            account, repo, name, version = ss
        else:
            raise ValueError("format of the template uid (%s) not valid" % uid)

        return cls(host, account, repo, name, version)

    def tuple(self):
        return (self.host, self.account, self.repo, self.name, self.version)

    def __repr__(self):
        return '/'.join(self.tuple())

    def __str__(self):
        return repr(self)

    def __comp(self, other):
        if self.tuple()[:-1] != other.tuple()[:-1]:
            raise ValueError("other is not the same template, can't compare version")
        if self.version < other.version:
            return -1
        elif self.version > other.version:
            return 1
        else:
            return 0

    def __eq__(self, other):
        if not isinstance(other, TemplateUID):
            raise ValueError("other is not an instance of TemplateUID")

        return self.tuple() == other.tuple()

    def __lt__(self, other):
        return self.__comp(other) == -1

    def __le__(self, other):
        return self.__comp(other) in [0, -1]

    def __gt__(self, other):
        return self.__comp(other) == 1

    def __ge__(self, other):
        return self.__comp(other) in [0, 1]

    def __hash__(self):
        return hash(self.tuple())