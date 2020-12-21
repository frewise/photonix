import React from 'react'
import styled from '@emotion/styled'

import Thumbnail from '../Thumbnail/index.js'


const Container = styled('ul')`
  margin: 0;
  padding: 0;
  & > h2 {
    display: block;
  }
`
const SectionHeading = styled('h2')`
  display: block;
`

const Thumbnails = ({ photoSections }) => (
  <Container>
    {
      photoSections ?
      photoSections.map((section) => {
        return (
          <div className="section" id={section.id} key={section.id}>
            { section.title ? <SectionHeading>{section.title}</SectionHeading> : null }
            {
              section.segments.map((segment) => (
                segment.photos.map((photo) => (
                  <Thumbnail id={photo.id} imageUrl={photo.thumbnail} />
                ))
              ))
            }
          </div>
        )
      })
      : null
    }
  </Container>
)

export default Thumbnails