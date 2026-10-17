# Private submodule

The owner selected `N4M3Z/lsrules-private` as the private companion repository.
Its public declaration uses the path `private/` and the URL `https://github.com/N4M3Z/lsrules-private.git`.
The parent exposes this URL and the selected commit. GitHub access controls protect the private contents.
See the [Git submodule documentation](https://git-scm.com/docs/gitsubmodules).

## Content boundary

Keep reusable policy and procedures in the public parent.
Keep reviewed personal policy, private work, and approved exceptions in the private repository.
Keep credentials in the existing credential store. Do not place them in either repository.
Native backups, addresses, network names, inventories, and detailed evidence remain local until their exact upload scope receives owner approval.

The private repository starts with a minimal scaffold. It contains no machine data at bootstrap.
The public EUPL license does not license private companion data.

## Clone behavior

Use a normal clone for the public repository. Do not initialize submodules automatically.
The public validator accepts an absent private checkout with the exact reviewed submodule declaration.
An authorized owner can initialize only the private submodule:

```sh
git submodule update --init -- private
```

Do not put a token in the submodule URL.
Use the existing authenticated Git workflow when private access is required.

## Local source boundary

The existing source checkout uses Jujutsu.
Jujutsu does not support submodule edits. See its [Git compatibility documentation](https://docs.jj-vcs.dev/latest/git-compatibility/).
Prepare the actual submodule in a separate Git publication checkout.
Preserve the original checkout and its Git and Jujutsu metadata.
The submodule declaration alone does not establish a linked child commit.

## Publication checks

Verify the private repository visibility before its first upload.
Verify the child commit before recording its gitlink in the parent.
Keep the URL, submodule path, and selected commit in the reviewed public publication manifest.
Exclude every private payload file from public scans and archives.
The validator must reject unexpected submodule URLs, paths, symlinks, and ordinary directories presented as private submodules.

Do not publish old parent history or private evidence.
Do not treat a successful secret scan as proof that all personal information is absent.
The public parent still requires exact approval before its commit and publication.
