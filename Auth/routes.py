from flask import Blueprint, render_template, request, flash, redirect, url_for, session

auth = Blueprint("auth", __name__, url_prefix="/auth")