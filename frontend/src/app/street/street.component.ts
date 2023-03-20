import { Component, Input, OnInit } from '@angular/core';
import { Street } from '../dto/street';

@Component({
  selector: 'app-street',
  templateUrl: './street.component.html',
  styleUrls: ['./street.component.css']
})
export class StreetComponent implements OnInit {
  @Input() street?: Street

  constructor() { }

  ngOnInit(): void {
  }

}
