import os

import click

from myday import core


@click.group()
@click.pass_context
def main(ctx):
    org = os.path.expanduser("~/Dropbox/zzOrg")
    files = sorted([os.path.join(org, f) for f in os.listdir(org)
                    if f.endswith('.org')])

    ctx.obj = {'db': core.OrgDB(*files)}


@main.command()
@click.pass_context
def start(ctx):
    core.reset_dailies(ctx.obj['db'])
    click.echo("Ready to start the day! Here are your dailies.")
    ctx.invoke(dailies, showdone=False)


@main.command()
@click.option('--showdone', is_flag=True)
@click.pass_context
def dailies(ctx, showdone):
    todo, done = core.dailies(ctx.obj['db'])

    if len(todo) == 0:
        click.echo("No uncompleted tasks for today. Great job!")

    for i, el in enumerate(todo):
        click.echo("%d. %s" % (i+1, el.headline))
    if showdone:
        click.echo("--- Completed tasks ---")
        for el in done:
            click.echo(el.headline)


@main.command()
@click.argument('task')
@click.pass_context
def done(ctx, task):
    try:
        # If user gives us an int, it will be a daily index + 1
        task = "%d" % (int(task) - 1)
    except ValueError:
        pass
    core.mark_done(ctx.obj['db'], task)
    ctx.invoke(dailies, showdone=True)


@main.command()
@click.argument('project')
@click.pass_context
def task(ctx, project):
    pass


@main.command()
@click.pass_context
def end(ctx):
    click.echo("Summary of the day...")
    ctx.invoke(dailies, showdone=True)
    core.reset_dailies(ctx.obj['db'])

if __name__ == '__main__':
    main()
