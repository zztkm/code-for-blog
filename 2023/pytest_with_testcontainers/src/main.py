import argparse


def develop():
    import uvicorn

    uvicorn.run("udonya:app", host="localhost", port=8080, reload=True)


def production():
    import uvicorn

    uvicorn.run("udonya:app", host="localhost", port=8080, reload=False)


def main():
    parser = argparse.ArgumentParser(description="udonya api manager")
    sub = parser.add_subparsers()

    # develop
    dev = sub.add_parser("dev")
    dev.set_defaults(handler=develop)

    # production
    prod = sub.add_parser("prod")
    prod.set_defaults(handler=production)

    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
